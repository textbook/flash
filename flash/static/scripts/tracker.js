function trackerUpdate () {
  $.getJSON($SERVICES, {name: 'tracker'}, function (data) {
    if (data) {
      console.debug('received Tracker data', data);
      if (data.name) { $('#tracker-service .project-name').text(data.name); }
      if (data.velocity){ $('.tracker-pane .velocity').text(data.velocity); }
      lastUpdate('#tracker-service');
    }
  });
}

$(document).ready(function () {
  trackerUpdate();
  setInterval(trackerUpdate, $MINUTE);
});
