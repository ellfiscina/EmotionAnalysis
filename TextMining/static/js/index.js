$(document).ready(function() {
  $('input:file').change(
    function(){
      if ($(this).val()) {
        $('input:submit').attr('disabled',false);
          // or, as has been pointed out elsewhere:
          // $('input:submit').removeAttr('disabled');
      }
    }
  );
});
