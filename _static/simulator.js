$(function() {
   $('a.armcode').on('click', function(event) {
      event.preventDefault();

      var code_id= $(this).data( "for");
      var code_block = $("#" + code_id);
      var data = new FormData();
      data.append('file', new Blob([code_block.text()]), 'asmbits');

      var xhr = new XMLHttpRequest();
      xhr.open("POST", "https://cpulator.01xz.net/share.php");
      xhr.responseType = "text";
      xhr.onload = function() {
         var new_url = "https://cpulator.01xz.net/?loadasm=share/" + xhr.response.trim();
         new_url = new_url + (String.fromCharCode(0x26) + "sys=arm");
         window.open(new_url);
      }
      xhr.send(data);
   });
});
