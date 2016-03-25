const MINUTE = 1000 * 60;

function formattedDate() {
  var date = new Date();
  return date.toDateString() + ' ' + date.toLocaleTimeString();
}

function trackerUpdate () {
  $.getJSON($SERVICES, {name: 'tracker'}, function (data) {
    if (data) {
      console.debug('received data', data);
      if (data.name) { $('.tracker-pane .project-name').text(data.name); }
      if (data.velocity){ $('.tracker-pane .velocity').text(data.velocity); }
      $('.last-update').text(formattedDate())
    }
  });
}

function codeshipUpdate () {
  $.getJSON($SERVICES, {name: 'codeship'}, function (data) {
    if (data) {
      console.debug('received data', data);
      if (data.repository_name) {
        $('.codeship-pane .project-name').text(data.repository_name);
      }
      if (data.builds) {
        console.log('iterating', data.builds.slice(0, 4));
        for (var index in data.builds.slice(0, 4)) {
          var build = data.builds[index];
          $('.codeship-pane #outcome-' + index).text(build.status)
        }
      }
      $('.last-update').text(formattedDate())
    }
  });
}

function updateAll() {
  codeshipUpdate();
  trackerUpdate();
}

$(document).ready(function () {
  updateAll();
  setInterval(updateAll, MINUTE);
});
