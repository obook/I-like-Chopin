'use strict';

(() => {

    /* Init */
    if (!localStorage.getItem('last_song_uuid')) {
        localStorage.setItem('last_song_uuid', '0');
    }

    /* Helpers */
    const isWindowsPath = (filePath = '') => filePath.length > 1 && filePath[1] === ':';

    const removeSongnameClasses = (selector) => {
        const classes = [
            'class_songname_0',
            'class_songname_1',
            'class_songname_2',
            'class_songname_3',
            'class_songname_unknown',
            'class_songname_error'
        ];
        classes.forEach(c => $(selector).removeClass(c));
    };

    const setPageTextEmpty = () => {
        $('#songname').text('...');
        $('#folder').text('');
        $('#info_line').text('');
        $('#progressbar').val(0);

        $('#songname_page2').text('...');
        $('#folder_page2').text('');
        $('#info_line_page2').text('');
        $('#progressbar_page2').val(0);
    };

    /* Fullscreen */
    window.toggleFullScreen = () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
            localStorage.setItem('fullscreen', 'true');
        } else if (document.exitFullscreen) {
            document.exitFullscreen();
            localStorage.setItem('fullscreen', 'false');
        }
        $('#panel_right').panel('close');
    };

    /* Play a file (click) */
    window.PlaySong = async (song) => {
        ShowLoader();
        removeSongnameClasses('#songname');
        removeSongnameClasses('#songname_page2');
        setPageTextEmpty();

        try {
            await fetch(`/play?song=${song}`);
        } catch (err) {
            console.error('PlaySong error', err);
        } finally {
            $('#panel_left').panel('close');
            $('#panel_right').panel('close');
        }
    };

    /* Order action (navbar) */
    window.OrderDo = async (action) => {
        ShowLoader();
        try {
            await fetch(`/do?action=${action}`);
            TimerGetStats();
        } catch (err) {
            console.error('OrderDo error', err);
        }
    };

    /* Mode select changed */
    $('#select-mode').on('change', function () {
        ShowLoader();
        const mode = $(this).val();
        fetch(`/player?mode=${mode}`).catch(err => console.error('select-mode error', err));
    });

    /* Add current song to playlist */
    window.PlayListAdd = () => {
        const quality = $('#select-stars').find(':selected').val();
        fetch(`/add?quality=${quality}`).catch(err => console.error('PlayListAdd error', err));
        GetPlaylist();
    };

    /* Button colors */
    function SetButtonColors(ready = true) {
        if (ready) {
            $('#id_songname').css('background', 'green');
        } else {
            $('#id_songname').css('background', 'red');
        }
    }

    function ShowLoader() {
        SetButtonColors(false);
        $.mobile.loading('show', {
            text: 'Loading...',
            textonly: false,
            textVisible: true,
            theme: 'a',
            html: ''
        });
    }

    /* API / UI updates */
    async function TimerGetStats() {
        $.mobile.loading('hide');

        try {
            $('.ui-btn-active').removeClass('ui-btn-active');

            const response = await fetch('/status.json');
            const data = await response.json();

            const song_uuid = data.uuid;
            const last_song_uuid = localStorage.getItem('last_song_uuid');

            if (song_uuid !== last_song_uuid) {
                console.log(`New song uuid=${song_uuid}`);
                localStorage.setItem('last_song_uuid', song_uuid);
                removeSongnameClasses('#songname');
                removeSongnameClasses('#songname_page2');
                setPageTextEmpty();

                SetScore(data.score);
                SetButtonColors(true);
            }

            $('#songname').text(data.nameclean);
            $('#songname_page2').text(data.nameclean);
            document.title = data.nameclean;

            $('#score').attr('href', `../score?pdf=${data.score}#view=FitH`);
            $('#folder').text(data.folder);
            $('#folder_page2').text(data.folder);

            let channels = ' ';
            for (const [key] of Object.entries(data.channels || {})) {
                const channel = parseInt(key, 10) + 1;
                channels += `${channel} `;
            }

            const minutes = Math.floor(data.duration);
            const seconds = Math.floor((data.duration - minutes) * 60);
            let line = `${minutes}'${String(seconds).padStart(2, '0')}`;
            line += data.sustain > 0 ? ' 𝄞' : ' ❌';
            line += ` [${channels}]`;

            $('#info_line').text(line);
            $('#info_line_page2').text(line);

            $('#progressbar').val(data.played);
            $('#progressbar_page2').val(data.played);

            if (data.state < 0) {
                $('#songname').addClass('class_songname_error');
                $('#songname_page2').addClass('class_songname_error');
            }

            if (data.state === -4) {
                $('#info_line').text('! NO ACTIVE TRACK TO PLAY');
                SetButtonColors(false);
            } else if (data.state < 2) {
                $('#songname').addClass('class_songname_unknown');
                $('#songname_page2').addClass('class_songname_unknown');
                SetButtonColors(false);
            } else {
                SetButtonColors(true);
                const mode = data.mode;
                if (mode === 2) {
                    $('#songname').addClass('class_songname_2');
                    $('#songname_page2').addClass('class_songname_2');
                } else if (mode === 3) {
                    $('#songname').addClass('class_songname_3');
                    $('#songname_page2').addClass('class_songname_3');
                } else if (mode === 4) {
                    $('#songname').addClass('class_songname_0');
                    $('#songname_page2').addClass('class_songname_0');
                } else {
                    $('#songname').addClass('class_songname_1');
                    $('#songname_page2').addClass('class_songname_1');
                }
            }

            if (data.mode === 1) {
                $('#select-mode').val('playback').selectmenu('refresh');
            } else if (data.mode === 2) {
                $('#select-mode').val('passthrough').selectmenu('refresh');
            } else if (data.mode === 3) {
                $('#select-mode').val('player').selectmenu('refresh');
            } else if (data.mode === 4) {
                $('#select-mode').val('random').selectmenu('refresh');
            } else {
                $('#select-mode').val('playback').selectmenu('refresh');
            }

        } catch (error) {
            console.log('---> NETWORK ERROR : ', error);
            $('#songname').addClass('class_songname_error').text('OFFLINE');
            $('#folder').text('');
            $('#info_line').text('');
            $('#progressbar').val(0);
        }
    }

    async function GetFiles() {
        try {
            const response = await fetch('/files.json');
            const data = await response.json();

            let html = "<div data-role='collapsibleset' data-theme='b' data-inset='false' data-collapsed-icon='false'>";

            for (const artist in data) {
                html += `<div data-role='collapsible'>
<h2>${artist}</h2>
<ul data-role='listview' data-autodividers='true'>`;

                for (const midifiles in data[artist]) {
                    const filePath = data[artist][midifiles];
                    const filePath_URI = encodeURIComponent(filePath).replace(/'/g, '%27');

                    const pathStrSplit = isWindowsPath(filePath)
                        ? filePath.split('\\').pop().split('/')
                        : filePath.split('/');

                    const fileName = pathStrSplit.pop();
                    let fileNameShort = fileName.substring(0, fileName.lastIndexOf('.')) || fileName;
                    fileNameShort = fileNameShort.replaceAll('_', ' ').replaceAll('-', ' ').replaceAll(',', '');

                    html += `<li class='class_filename' data-theme='a'>
<a href='#' onclick='PlaySong("${filePath_URI}");'>${fileNameShort}</a>
</li>`;
                }

                html += '</ul></div>';
            }

            html += '</div>';
            $('#files_list').append(html).trigger('create');

        } catch (error) {
            console.error('---> NETWORK ERROR : ', error);
        }
    }

    async function GetPlaylist() {
        if (document.getElementById('playlisy_ul')) {
            $('#files_playlist').empty().trigger('create');
        }

        try {
            const response = await fetch('/playlist.json');
            const data = await response.json();

            let html = `<ul data-role='listview' data-theme='b' id='playlisy_ul'>
<li data-role="list-divider" data-theme='a'>PLAYLIST</li>`;

            $.each(data, function (_index, item) {
                const filePath_URI = encodeURIComponent(item.path).replace(/'/g, '%27');
                html += `<li data-icon='false'>
<a href='#' onclick='PlaySong("${filePath_URI}");'>${item.title}</a>
</li>`;
            });

            html += '</ul>';
            $('#files_playlist').append(html).trigger('create');

        } catch (error) {
            console.error('---> NETWORK ERROR : ', error);
        }
    }

    async function SetQRCode() {
        try {
            const response = await fetch('/interfaces.json');
            const data = await response.json();

            for (const iface in data) {
                const url = data[iface];
                if (!url.includes('127.0.0.1')) {
                    $('#qrcode').append(`<p>${url}</p>`);
                    /* QRCode global assumed available */
                    /* eslint-disable-next-line no-undef */
                    new QRCode(document.getElementById('qrcode'), url);
                }
            }
        } catch (error) {
            console.error('---> NETWORK ERROR : ', error);
        }
    }

    function SetScore(scorefile) {
        $('#pdftarget embed').attr('src', `../score?pdf=${scorefile}`).trigger('create');
    }

    /* Main */
    SetQRCode();
    GetFiles();
    GetPlaylist();
    SetButtonColors(false);
    TimerGetStats();
    setInterval(TimerGetStats, 2000);

    /* Expose some functions for inline onclick usage (already set on window above) */
})();
