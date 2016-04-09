/* global $, setTileHealth, updateItems, $MINUTE */

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
      setTileHealth($('#travis-service'), data.health || 'neutral');
    }
  });
}

$(document).ready(function () {
  travisUpdate();
  setInterval(travisUpdate, $MINUTE);
});
