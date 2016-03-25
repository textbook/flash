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
      var date = new Date();
      $('.last-update').text(
        date.toDateString() + ' ' + date.toLocaleTimeString()
      )
    }
  });
}

$(document).ready(function () {
  codeshipUpdate();
  setInterval(codeshipUpdate, $MINUTE);
});
