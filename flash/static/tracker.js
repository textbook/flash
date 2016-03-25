function trackerUpdate () {
  $.getJSON($SERVICES, {name: 'tracker'}, function (data) {
    if (data) {
      console.debug('received data', data);
      if (data.name) { $('.tracker-pane .project-name').text(data.name); }
      if (data.velocity){ $('.tracker-pane .velocity').text(data.velocity); }
      var date = new Date();
      $('.last-update').text(
        date.toDateString() + ' ' + date.toLocaleTimeString()
      )
    }
  });
}

$(document).ready(function () {
  trackerUpdate();
  setInterval(trackerUpdate, $MINUTE);
});
