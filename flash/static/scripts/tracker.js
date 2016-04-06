function trackerUpdate () {
  $.getJSON($SERVICES, {name: 'tracker'}, function (data) {
    if (data) {
      console.debug('received Tracker data', data);
      if (data.name) { $('#tracker-service .project-name').text(data.name); }
      if (data.velocity) { $('.tracker-pane .velocity').text(data.velocity); }
      if (data.stories) {
        $('.tracker-pane .accepted').text(data.stories.accepted || 0);
        $('.tracker-pane .in-flight').text(data.stories.started || 0);
        $('.tracker-pane .completed').text(
          (data.stories.finished || 0) + (data.stories.delivered || 0)
        );
      }
    }
  });
}

$(document).ready(function () {
  trackerUpdate();
  setInterval(trackerUpdate, $MINUTE);
});
