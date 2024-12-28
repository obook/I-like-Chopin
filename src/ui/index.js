
/* Global variables */

last_song_uuid = "";
last_song_nameclean = ""; /* Eg "CHIQUITITA" NOT USED */
last_song_folder = ""; /* Eg "ABBA" NOT USED */
last_song_name = ""; /* Eg "Chiquitita.mid" NOT USED */

/* Detect Windows */
function IsWindowsPath(filePath) {
    if (filePath.length>1) {
        if (filePath[1]==':') { /* Windows */
            return (true);
        }
    }
return (false);
}

/* Click on FullScreen */
function toggleFullScreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
        localStorage.setItem('fullscreen',true);
    } else if (document.exitFullscreen) {
        document.exitFullscreen();
        localStorage.setItem('fullscreen',false);
    }

    $('#panel_right').panel("close");
}

/* Click on file */
async function PlaySong(song) {
    ShowLoader();
    CleanSongName(true);
    const response = await fetch('/play?song='+song);
    /* Close all panels */
    $('#panel_left').panel("close");
    $('#panel_right').panel("close");
}

/* Click on navbar button */
async function OrderDo(action) {
    ShowLoader();
    const response = await fetch('/do?action='+action);
    GetStats();
}

/* Select mode changed */
$('#select-mode').change(function () {
    ShowLoader();
    const mode = $(this).val();
    const response = fetch('/player?mode='+mode);
});

/* Add current song to playlist */
function PlayListAdd() {
    let quality = $('#select-stars').find(":selected").val(); /* Eg 'star4' */
    const response = fetch('/add?quality='+quality);
}

/* Clean songname style */
function CleanSongName(empty_strings=false) {
    $("#songname").removeClass("class_songname_0");
    $("#songname").removeClass("class_songname_1");
    $("#songname").removeClass("class_songname_2");
    $("#songname").removeClass("class_songname_3");
    $("#songname").removeClass("class_songname_unknown");
    $("#songname").removeClass("class_songname_error");
    if(empty_strings==true) {
        $('#songname').text("...");;
        $('#folder').text("");
        $('#info_line').text("");
        $('#progressbar').val(0);
    }
}

function ShowLoader() {
    $.mobile.loading( "show", {
        text: "Loading...",
        textonly: false,
        textVisible: true,
        theme: "a",
        html: ""
      });
}

/* Tools */

function NameShort(filepath) { /* not used */

    var fileNameShort=filepath.substring(0,filepath.lastIndexOf("."));
    fileNameShort = fileNameShort.replaceAll("_"," ");
    fileNameShort = fileNameShort.replaceAll("-"," ");
    fileNameShort = fileNameShort.replaceAll(",","");
    return(fileNameShort);
}

/* API */
async function GetStats() {

    $.mobile.loading( "hide" );

    try {

        $(".ui-btn-active").removeClass('ui-btn-active');

        const response = await fetch('/status.json');
        const data = await response.json();

        /* debug
        console.log("DEBUG GetStats=");
        console.log(data);
        */

        /* uuid */
        song_uuid = data.uuid;

        if(song_uuid != last_song_uuid)  { /* New song */
            CleanSongName(true);
        }
        else {
            last_song_uuid = song_uuid;
        }

        /* Song Name */
        $('#songname').text(data.nameclean);
        document.title = data.nameclean;

        last_song_nameclean = data.nameclean; /* Eg "CHIQUITITA" */
        last_song_folder = data.folder; /* Eg "ABBA" */
        last_song_name = data.name; /* Eg "Chiquitita.mid" */

        /* Music sheet
        Add +'#option1=value&option2=value...'

        toolbar=1' : title in brave, no effect with firefox
        toolbar=0' : remove toolbar in brave, no effect with firefox

        pagemode=thumbs : is default for brave, is not per default with firefox
        pagemode=bookmarks : is default for brave, is not per default with firefox
        pagemode=none : ?

        view=FitH : ok Brave, notok Firefox

        $('#score').attr('href', "../score?pdf=" + data.score + '#view=FitH&toolbar=0&pagemode=thumbs');
        */
        $('#score').attr('href', "../score?pdf=" + data.score + '#view=FitH');

        /* Parent folder of MIDIfile */
        $('#folder').text(data.folder);

        /* Actives MIDI channels of MIDIfile */
        channels = " ";
        for (const [key, value] of Object.entries(data.channels)) {
            channel =  parseInt(key) + 1;
            channels = channels + channel + " ";
        }

        /* Duration */
        const minutes = Math.floor(data.duration);
        const seconds = Math.floor((data.duration - minutes)*60);
        line = minutes+"'"+String(seconds).padStart(2, '0');
        if(data.sustain > 0)
            line = line + " 𝄞"
        else
            line = line + " ❌"
        line = line + " ["+channels+"] ";
        $('#info_line').text(line);

        /* Progress bar */
        $('#progressbar').val(data.played);

        /* Handle MIDIfile states and errors */
        if (data.state <0) {
            $("#songname").addClass("class_songname_error"); /* Error */
        if  (data.state ==-4)  {/* no track to play */
            document.getElementById('info_line').textContent="! NO ACTIVE TRACK TO PLAY";
        }
        }
        else if (data.state <2) /* state 1 or 2 unknown or cueing */
            $("#songname").addClass("class_songname_unknown"); /* Unknown */
        else { /* state 2,3 = ready or playing */
            if (data.mode == 2)
            $("#songname").addClass("class_songname_2"); /* Passthrough */
            else if (data.mode == 3)
            $("#songname").addClass("class_songname_3"); /* Player Playing*/
            else if (data.mode == 4)
            $("#songname").addClass("class_songname_0"); /* Random Playing */
            else
            $("#songname").addClass("class_songname_1");/* Ready/Playing */
        }

        /* Mode */
        if (data.mode == 1)
            $('#select-mode').val("playback").selectmenu('refresh');
        else if (data.mode == 2)
            $('#select-mode').val("passthrough").selectmenu('refresh');
        else if (data.mode == 3)
            $('#select-mode').val("player").selectmenu('refresh');
        else if (data.mode == 4)
            $('#select-mode').val("random").selectmenu('refresh');
        else
            $('#select-mode').val("playback").selectmenu('refresh');

    } catch (error) {
        console.error('---> NETWORK ERROR : ', error);
        $("#songname").addClass("class_songname_error");
        $('#songname').text("OFFLINE");;
        $('#folder').text("");
        $('#info_line').text("");
        $('#progressbar').val(0);
    }
}

async function GetFiles() {
    try {
        const response = await fetch('/files.json');
        const data = await response.json();

        /* console.log(data); */

        html = "<div data-role='collapsibleset' data-theme='b' data-inset='false' data-collapsed-icon='false'>";

        for(var artist in data) {

            html = html + `<div data-role='collapsible'>\n` +
            `<h2>${artist}</h2>\n` +
            `<ul data-role='listview' data-autodividers='true'>\n`;

            for (var midifiles in data[artist]) {
                const filePath = data[artist][midifiles];
                const filePath_URI = encodeURIComponent(filePath).replace(/'/g, "%27"); // Encode for make an URL

                if ( IsWindowsPath(filePath) == true) {
                    var pathStrSplit= filePath.split('\\').pop().split('/'); // Windows
                }
                else {
                    var pathStrSplit = filePath.split('/'); // POSIX
                }

                const fileName = pathStrSplit.pop();
                var fileNameShort=fileName.substring(0,fileName.lastIndexOf("."));
                fileNameShort = fileNameShort.replaceAll("_"," ");
                fileNameShort = fileNameShort.replaceAll("-"," ");
                fileNameShort = fileNameShort.replaceAll(",","");

                html = html + ` <li class='class_filename' data-theme='a'>` +
                `<a href='#' onclick='PlaySong("${filePath_URI}");'>${fileNameShort}</a>` +
                `</li>\n`;

                /* NOT USED : because NEW VOTE BUTTON
                html = html + ` <li class='class_filename' data-theme='a' data-icon='plus'>` +
                `<a href='#' onclick='PlaySong("${filePath_URI}");'>${fileNameShort}</a>` +
                `<a href='#playlist_add' data-rel='popup' data-position-to='window' data-transition='pop'>Purchase album</a>`+
                `</li>\n`;
                */
            }

            html = html +"</ul>\n</div>\n";
        }

        html = html + "</div>\n";

        $("#files_list").append(html).trigger( "create" );

    } catch (error) {
            console.error('---> NETWORK ERROR : ', error);
    }

}

async function GetPlaylist(){

    try {
        const response = await fetch('/playlist.json');
        const data = await response.json();

        html = `<ul data-role='listview' data-theme='b'>\n`;
        html = html + `<li data-role="list-divider" data-theme='a'>PLAYLIST</li>\n`;

        $.each(data,function(index,item){
            /*
            console.log("artist = " + item.artist);
            console.log("title = " + item.title);
            console.log("path = " + item.path);
            console.log("**************");
            */
            const filePath_URI = encodeURIComponent(item.path).replace(/'/g, "%27"); // Encode for make an URL

            html = html + `<li data-icon='false'>` +
            `<a href='#' onclick='PlaySong("${filePath_URI}");'>${item.title}</a>` +
            `</li>\n`;
        });

        html = html + "</ul>\n";

        $("#files_playlist").append(html).trigger( "create" );

    } catch (error) {
            console.error('---> NETWORK ERROR : ', error);
    }

}


/* QRCode */
async function SetQRCode(){

    // console.log("SetQRCode")

    try {
        const response = await fetch('/interfaces.json');
        const data = await response.json();

        for(var interface in data) {
            url = data[interface]
            if(!url.includes("127.0.0.1"))
                new QRCode(document.getElementById("qrcode"), url);
        }

    } catch (error) {
            console.error('---> NETWORK ERROR : ', error);
    }
    /* QRCode */

}

/* Main script */
SetQRCode();
GetFiles();
GetStats();
GetPlaylist();
setInterval(GetStats, 2000);
