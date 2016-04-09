var updateCommit = function(element, data) {
  ['author', 'committed', 'message'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
};

var updateOutcome = function(element, data) {
  element.removeClass('passed failed crashed cancelled working');
  element.addClass(data.outcome);
  ['author', 'elapsed', 'message', 'outcome'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
};

var updateItems = function(pane, items, selector, updater) {
  var elements = pane.children(selector);
  items.slice(0, 4).forEach(function (item, index) {
    updater(elements.eq(index), item);
  });
};

var setTileHealth = function(tile, health) {
  tile.removeClass('tile-ok tile-error');
  if (health === 'ok') {
    tile.addClass('tile-ok');
  } else if (health === 'error') {
    tile.addClass('tile-error');
  }
};
