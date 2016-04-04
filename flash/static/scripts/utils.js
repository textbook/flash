function lastUpdate (paneSelector, updated) {
  $(paneSelector + ' .last-update').text('Last update: ' + (updated || 'unknown'));
}

function updateCommit (element, data) {
  ['author', 'committed', 'message'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
}

function updateOutcome (element, data) {
  element.removeClass('passed failed crashed cancelled working');
  element.addClass(data.outcome);
  ['author', 'elapsed', 'message', 'outcome'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
}

function updateItems(pane, items, selector, updater) {
  var elements = pane.children(selector);
  items.slice(0, 4).forEach(function (item, index) {
    updater(elements.eq(index), item);
  });
}
