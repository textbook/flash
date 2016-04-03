function githubUpdate () {
  $.getJSON($SERVICES, {name: 'github'}, function (data) {
    if (data) {
      var pane = $('section.github-pane');
      console.debug('received GitHub data', data);
      if (data.name) {
        $('#github-service').children('.service-caption').children('.project-name').text(
          data.name
        );
      }
      if (data.commits) {
        updateItems(pane, data.commits, '.commit', updateCommit);
      }
      lastUpdate('#github-service');
    }
  });
}

$(document).ready(function () {
  githubUpdate();
  setInterval(githubUpdate, $MINUTE);
});
