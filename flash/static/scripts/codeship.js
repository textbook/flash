function codeshipBuildData (build) {
  return {
    author: build.github_username,
    end: build.finished_at,
    message: build.message,
    outcome: build.status,
    start: build.started_at
  };
}

function codeshipUpdate () {
  $.getJSON($SERVICES, {name: 'codeship'}, function (data) {
    if (data) {
      var pane = $('section.codeship-pane');
      console.debug('received data', data);
      if (data.repository_name) {
        $('#codeship-service').children('.service-caption').children('.project-name').text(
          data.repository_name
        );
      }
      if (data.builds) {
        updateOutcomes(pane, data.builds, codeshipBuildData);
      }
      lastUpdate('#codeship-service');
    }
  });
}

$(document).ready(function () {
  codeshipUpdate();
  setInterval(codeshipUpdate, $MINUTE);
});
