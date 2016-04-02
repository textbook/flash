function lastUpdate (paneSelector) {
  var now = new Date();
  $(paneSelector + ' .last-update').text(
    'Last update: ' + now.toDateString() + ' ' + now.toLocaleTimeString()
  );
}

function updateOutcome (element, data) {
  element.removeClass('success error');
  element.addClass(data.outcome);
  ['author', 'elapsed', 'message', 'outcome'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
}

function updateOutcomes(pane, builds) {
  var outcomes = pane.children('.build-outcome');
  builds.slice(0, 4).forEach(function (build, index) {
    updateOutcome(outcomes.eq(index), build);
  });
}
