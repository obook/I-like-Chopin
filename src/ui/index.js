/* Click on file */
function PlaySong(song) {
    console.log("PLAY->"+song);
    fetch('http://127.0.0.1:8888?play='+song);
}

/* Click on button */
function Do(order) {
    /* ShowLoader();
    fetch('?do='+order); */
    console.log("Do="+order);
    fetch('http://127.0.0.1:8888/?do='+order);
    getStats();
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
}

/* Clean songname style */
function CleanSongName() {
    $("#songname").removeClass("class_songname_0");
    $("#songname").removeClass("class_songname_1");
    $("#songname").removeClass("class_songname_2");
    $("#songname").removeClass("class_songname_3");
    $("#songname").removeClass("class_songname_unknown");
    $("#songname").removeClass("class_songname_error");
    /* $("#songname").addClass("class_songname_0");  */
}

/* API */
async function getStats() {

try {

    $(".ui-btn-active").removeClass('ui-btn-active');

    /* const response = await fetch('status.json'); */
    const response = await fetch('http://127.0.0.1:8888/status.json');
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
    line = line + " ["+channels+"] ";
    if(data.sustain > 0)
    line = line + "🎹"
    else
    line = line + "💻"
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

    } catch (error) {
    console.error('---> NETWORK ERROR : ', error);
    }
}

async function getSgetFiles() {

    /* try { */
        const response = await fetch('http://127.0.0.1:8888/files.json');
        const data = await response.json();

        html = "<div data-role='collapsibleset' data-theme='b' data-inset='false'>";
        for(var artist in data) {

            html = html + "<div data-role='collapsible'><h2>"+artist+"</h2><ul data-role='listview'>";
            for (var midifiles in data[artist]) {
                filePath = data[artist][midifiles];
                const pathStrSplit = filePath.split('/'); /* !!!!!!! NOT WINDOWS COMPATIBLE */
                const fileName = pathStrSplit.pop();
                var fileNameShort=fileName.substring(0,fileName.lastIndexOf("."));
                fileNameShort = fileNameShort.replaceAll("_"," ");
                fileNameShort = fileNameShort.replaceAll("-"," ");
                fileNameShort = fileNameShort.replaceAll(",","");
                /*fileNameShort = fileNameShort.replaceAll("'",""); */
                html = html + " <li data-theme='a' data-icon='false'><a href='#' onclick='PlaySong(\""+escape(filePath)+"\");'>"+fileNameShort+"</a></li>"; /* !! escape is obsolete */
            }

            html = html +"</ul></div>";
        }

        html = html + "</div>";

        $("#files_list").append(html).trigger( "create" );

   /* } catch (error) {
            console.error('---> NETWORK ERROR : ', error);
    }*/
}

/* Main script */
getSgetFiles();
getStats();
setInterval(getStats, 2000);
