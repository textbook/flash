function travisUpdate () {
  $.getJSON($SERVICES, {name: 'travis'}, function (data) {
    if (data) {
      var pane = $('section.travis-pane');
      console.debug('received Travis data', data);
      if (data.name) {
        $('#travis-service').children('.service-caption').children('.project-name').text(
          data.name
        );
      }
      if (data.builds) {
        updateItems(pane, data.builds, '.build-outcome', updateOutcome);
      }
      lastUpdate('#travis-service');
    }
  });
}

$(document).ready(function () {
  travisUpdate();
  setInterval(travisUpdate, $MINUTE);
});
