
first_run = false;

/* Click on FullScreen */
function toggleFullScreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
        localStorage.setItem('fullscreen',true);
    } else if (document.exitFullscreen) {
        document.exitFullscreen();
        localStorage.setItem('fullscreen',false);
    }
}

/* Click on file */
async function PlaySong(song) {
    CleanSongName();
    $('#songname').text("...");;
    $('#folder').text("");
    $('#duration').text("");
    $('#progressbar').val(0);
    ShowLoader();
    const response = fetch('/?play='+song);
}

/* Click on navbar button */
async function OrderDo(order) {
    ShowLoader();
    const response = fetch('/?do='+order);
    getStats();
}

/* Select mode changed */
$('#select-mode').change(function () {
    const mode = $(this).val();
    ShowLoader();
    fetch('/?mode='+mode);
});

/* Clean songname style */
function CleanSongName() {
    $("#songname").removeClass("class_songname_0");
    $("#songname").removeClass("class_songname_1");
    $("#songname").removeClass("class_songname_2");
    $("#songname").removeClass("class_songname_3");
    $("#songname").removeClass("class_songname_unknown");
    $("#songname").removeClass("class_songname_error");
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

/* API */
async function getStats() {

    $.mobile.loading( "hide" );

    /* test */

    $('#select-mode').val("player"); //.selectmenu('refresh');


    try {

        $(".ui-btn-active").removeClass('ui-btn-active');

        /* const response = await fetch('status.json'); */
        const response = await fetch('/status.json');
        const data = await response.json();

        /* Song Name */
        $('#songname').text(data.nameclean);
        document.title = data.nameclean;

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
            line = line + " 🎹"
        else
            line = line + " 💻"
        line = line + " ["+channels+"] ";
        $('#duration').text(line);

        /* Progress bar */
        $('#progressbar').val(data.played);

        /* Handle MIDIfile states and errors */

        CleanSongName();

        if (data.state <0) {
            $("#songname").addClass("class_songname_error"); /* Error */
        if  (data.state ==-4)  {/* no track to play */
            document.getElementById('duration').textContent="! NO ACTIVE TRACK TO PLAY";
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

        if(first_run != true) {
            first_run = true;
            /*
            getFiles();
            SetQRCode();
            */
        }

    } catch (error) {
        first_run = false;
        console.error('---> NETWORK ERROR : ', error);
        $("#songname").addClass("class_songname_error");
        $('#songname').text("OFFLINE");;
        $('#folder').text("");
        $('#duration').text("");
        $('#progressbar').val(0);
    }
}

async function getFiles() {
    try {
        const response = await fetch('/files.json');
        const data = await response.json();

        html = "<div data-role='collapsibleset' data-theme='b' data-inset='false' data-collapsed-icon='false'>";

        for(var artist in data) {

            html = html + "<div data-role='collapsible'>\n";
            html = html + "<h2>"+artist+"</h2>\n";
            html = html + "<ul data-role='listview' data-autodividers='true'>\n";

            for (var midifiles in data[artist]) {
                const filePath = data[artist][midifiles];
                const filePath_URI = encodeURIComponent(filePath).replace(/'/g, "%27");
                const pathStrSplit = filePath.split('/'); /* NOT WINDOWS COMPATIBLE ? */
                const fileName = pathStrSplit.pop();
                var fileNameShort=fileName.substring(0,fileName.lastIndexOf("."));
                fileNameShort = fileNameShort.replaceAll("_"," ");
                fileNameShort = fileNameShort.replaceAll("-"," ");
                fileNameShort = fileNameShort.replaceAll(",","");
                html = html + " <li data-theme='a' data-icon='audio'><a href='#' onclick='PlaySong( \""+filePath_URI+"\" );'>"+fileNameShort+"</a></li>\n";
            }

            html = html +"</ul>\n</div>\n";
        }

        html = html + "</div>\n";

        $("#files_list").append(html).trigger( "create" );

    } catch (error) {
            console.error('---> NETWORK ERROR : ', error);
    }

}

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
getFiles();
getStats();
setInterval(getStats, 2000);
