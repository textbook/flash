function codeshipUpdate () {
  $.getJSON($SERVICES, {name: 'codeship'}, function (data) {
    if (data) {
      var pane = $('section.codeship-pane');
      console.debug('received Codeship data', data);
      if (data.name) {
        $('#codeship-service').children('.service-caption').children('.project-name').text(
          data.name
        );
      }
      if (data.builds) {
        updateItems(pane, data.builds, '.build-outcome', updateOutcome);
      }
    }
  });
}

$(document).ready(function () {
  codeshipUpdate();
  setInterval(codeshipUpdate, $MINUTE);
});
