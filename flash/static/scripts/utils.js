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

/**
* This can be wrapped up in a jquery plugin.
* The current visual feedback is not great and will be improved.
*/
var bundleService = function (serviceSelector, interval) {
  console.log('bundle ', serviceSelector)
  var active = 0;
  var stacked = []
  var wrapper = bundle(serviceSelector);

  function bundle(selector) {
    var tiles = $(selector).remove();
    var wrapper = $('<div class="tiles-stack"></div>')

    tiles.each(function (index, obj) {
      stacked[index] = $(obj);
      stacked[index].append('<div class="tiles-count">' + (index + 1) + ' of ' + tiles.length+ '</div>');
      wrapper.append(stacked[index]);
    });
    $('.dashboard').append(wrapper);

    return wrapper;
  }

  function updateStacked() {
    if (stacked.length === 0) return;
    var currentActive = active++ % stacked.length;
    wrapper.children().hide();

    stacked[currentActive]
      .show()
      .effect('shake', {distance: 10, times: 3});
  }

  updateStacked();
  setInterval(updateStacked, interval)
}

$(document).ready(function () {
  bundleService('.tracker-tile', 10000);
  updateServices();
  setInterval(updateServices, 60000);
});
