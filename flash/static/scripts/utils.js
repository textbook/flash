/* globals $,$SERVICE_URL,SERVICES */

var setTileHealth = function(tile, health) {
  tile.removeClass('tile-ok tile-error');
  if (health === 'ok') {
    tile.addClass('tile-ok');
  } else if (health === 'error') {
    tile.addClass('tile-error');
  }
};

var updateCommit = function(element, data) {
  ['author', 'committed', 'message'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
};

var updateItems = function(pane, items, selector, updater) {
  var elements = pane.children(selector);
  items.slice(0, 4).forEach(function (item, index) {
    updater(elements.eq(index), item);
  });
};

var updateOutcome = function(element, data) {
  element.removeClass('passed failed crashed cancelled working');
  element.addClass(data.outcome);
  ['author', 'elapsed', 'message', 'outcome'].forEach(function (attr) {
    element.children('.' + attr).text(data[attr]);
  });
};

var processPayload = function (payload) {
  for (var key in payload) {
    if (payload.hasOwnProperty(key)) {
      var data = payload[key];
      var tile = $('#' + key);
      var pane = tile.children('.pane').first();
      var serviceHandler = SERVICES[data.service_name];

      setTileHealth(tile, data.health || 'neutral');
      tile.find('.service-caption > .project-name').first().text(data.name);

      if (serviceHandler && data) {
        serviceHandler(pane, data);
      }
    }
  }
};

var updateServices = function() {
  $.getJSON($SERVICE_URL, function (payload) {
    if (payload) {
      console.info('received', payload);
      processPayload(payload);
    }
  });
};

$(document).ready(function () {
  updateServices();
  setInterval(updateServices, 60000);
});

