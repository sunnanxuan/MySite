QUnit.module('Data adapters - Array');

var ArrayData = require('select2/data/array');
var $ = require('jquery');
var Options = require('select2/options');
var Utils = require('select2/utils');

var UserDefinedType = function (id, text) {
  var self = this;

  self.id = id;
  self.text = text;

  return self;
};

var arrayOptions = new Options({
  data: [
    {
      id: 'default',
      text: 'Default'
    },
    {
      id: '1',
      text: 'One'
    },
    {
      id: '2',
      text: '2'
    },
    new UserDefinedType(1, 'aaaaaa')
  ]
});

var extraOptions = new Options ({
  data: [
    {
      id: 'default',
      text: 'Default',
      extra: true
    },
    {
      id: 'One',
      text: 'One',
      extra: true
    }
  ]
});

var nestedOptions = new Options({
  data: [
    {
      text: 'Default',
      children: [
        {
          text: 'Next',
          children: [
            {
              id: 'a',
              text: 'Option'
            }
          ]
        }
      ]
    }
  ]
});

QUnit.test('current gets default for single', function (assert) {
  var $select = $('#qunit-fixture .single-empty');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  data.current(function (val) {
    assert.equal(
      val.length,
      1,
      'There should always be a selected item for array data.'
    );

    var item = val[0];

    assert.equal(
      item.id,
      'default',
      'The first item should be selected'
    );
  });
});

QUnit.test('current gets default for multiple', function (assert) {
  var $select = $('#qunit-fixture .multiple');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  data.current(function (val) {
    assert.equal(
      val.length,
      0,
      'There should be no default selection.'
    );
  });
});

QUnit.test('current works with existing selections', function (assert) {
  var $select = $('#qunit-fixture .multiple');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  $select.val(['One']);

  data.current(function (val) {
    assert.equal(
      val.length,
      1,
      'There should only be one existing selection.'
    );

    var option = val[0];

    assert.equal(
      option.id,
      'One',
      'The id should be equal to the value of the option tag.'
    );

    assert.equal(
      option.text,
      'One',
      'The text should be equal to the text of the option tag.'
    );
  });
});

QUnit.test('current works with selected data', function (assert) {
  var $select = $('#qunit-fixture .single-empty');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  data.select({
    id: '2',
    text: '2'
  });

  data.current(function (val) {
    assert.equal(
      val.length,
      1,
      'There should only be one option selected.'
    );

    var option = val[0];

    assert.equal(
      option.id,
      '2',
      'The id should match the original id from the array.'
    );

    assert.equal(
      option.text,
      '2',
      'The text should match the original text from the array.'
    );
  });
});

QUnit.test('select works for single', function (assert) {
  var $select = $('#qunit-fixture .single-empty');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  assert.equal(
    $select.val(),
    'default',
    'There should already be a selection'
  );

  data.select({
    id: '1',
    text: 'One'
  });

  assert.equal(
    $select.val(),
    '1',
    'The selected value should be the same as the selected id'
  );
});

QUnit.test('multiple sets the value', function (assert) {
  var $select = $('#qunit-fixture .multiple');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  assert.ok(
    $select.val() == null || $select.val().length == 0,
    'nothing should be selected'
  );

  data.select({
    id: 'default',
    text: 'Default'
  });

  assert.deepEqual($select.val(), ['default']);
});

QUnit.test('multiple adds to the old value', function (assert) {
  var $select = $('#qunit-fixture .multiple');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  $select.val(['One']);

  assert.deepEqual($select.val(), ['One']);

  data.select({
    id: 'default',
    text: 'Default'
  });

  assert.deepEqual($select.val(), ['One', 'default']);
});

QUnit.test('option tags are automatically generated', function (assert) {
  var $select = $('#qunit-fixture .single-empty');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  assert.equal(
    $select.find('option').length,
    4,
    'An <option> element should be created for each object'
  );
});

QUnit.test('automatically generated option tags have a result id', function (assert) {
  var $select = $('#qunit-fixture .single-empty');

  var data = new ArrayData($select, arrayOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  data.select({
    id: 'default'
  });

  assert.ok(
    Utils.GetData($select.find(':selected')[0], 'data')._resultId,
    '<option> default should have a result ID assigned'
  );
});

QUnit.test('option tags can receive new data', function(assert) {
  var $select = $('#qunit-fixture .single');

  var data = new ArrayData($select, extraOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  assert.equal(
    $select.find('option').length,
    2,
    'Only one more <option> element should be created'
  );

  data.select({
    id: 'default'
  });

  assert.ok(
    Utils.GetData($select.find(':selected')[0], 'data').extra,
    '<option> default should have new data'
  );

  data.select({
    id: 'One'
  });

  assert.ok(
    Utils.GetData($select.find(':selected')[0], 'data').extra,
    '<option> One should have new data'
  );
});

QUnit.test('optgroup tags can also be generated', function (assert) {
  var $select = $('#qunit-fixture .single-empty');

  var data = new ArrayData($select, nestedOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  assert.equal(
    $select.find('option').length,
    1,
    'An <option> element should be created for the one selectable object'
  );

  assert.equal(
    $select.find('optgroup').length,
    2,
    'An <optgroup> element should be created for the two with children'
  );
});

QUnit.test('optgroup tags have the right properties', function (assert) {
  var $select = $('#qunit-fixture .single-empty');

  var data = new ArrayData($select, nestedOptions);

  var container = new MockContainer();
  data.bind(container, $('<div></div>'));

  var $group = $select.children('optgroup');

  assert.equal(
    $group.prop('label'),
    'Default',
    'An `<optgroup>` label should match the text property'
  );

  assert.equal(
    $group.children().length,
    1,
    'The <optgroup> should have one child under it'
  );
});

QUnit.test('existing selections are respected on initialization', function (assert) {
   var $select = $(
     '<select>' +
        '<option>First</option>' +
        '<option selected>Second</option>' +
      '</select>'
    );

    var options = new Options({
      data: [
        {
          id: 'Second',
          text: 'Second'
        },
        {
          id: 'Third',
          text: 'Third'
        }
      ]
    });

    assert.equal($select.val(), 'Second');

    var data = new ArrayData($select, options);

    var container = new MockContainer();
    data.bind(container, $('<div></div>'));

    assert.equal($select.val(), 'Second');
});
