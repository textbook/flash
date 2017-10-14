from bs4 import BeautifulSoup


def test_undefined_section(jinja):
    context = _create_context('missing')
    expected = 'No pane template defined for missing service.'

    soup = _render(jinja, 'partials/undefined-section.html', context)

    assert soup.find('p', class_='warning').string.strip() == expected


def test_ci_section_without_builds(jinja):
    context = _create_context('fake-service', {'builds': []})
    soup = _render(jinja, 'partials/ci-section.html', context)

    assert 'fake-service-pane' in soup.find('section', class_='pane')['class']
    assert len(soup.find_all('div', class_='pane-item')) == 4


def test_ci_section_with_builds(jinja):
    builds = [
        _build('passed', 'Alice', 'took one minute', 'one'),
        _build('failed', 'Bob', 'took two minutes', 'two'),
        _build('crashed', 'Chris', 'took three minutes', 'three'),
        _build('working', 'Dipak', 'took four minutes', 'four'),
    ]
    context = _create_context('fake-service', {'builds': builds})

    soup = _render(jinja, 'partials/ci-section.html', context)

    assert 'fake-service-pane' in soup.find('section', class_='pane')['class']
    items = soup.find_all('div', class_='pane-item')
    _assert_contains(items, 'author', ['Alice', 'Bob', 'Chris', 'Dipak'])
    _assert_contains(items, 'message', ['one', 'two', 'three', 'four'])
    _assert_contains(
        items,
        'elapsed',
        [
            'took one minute',
            'took two minutes',
            'took three minutes',
            'took four minutes',
        ],
    )
    _assert_classes_contain(items, ['passed', 'failed', 'crashed', 'working'])


def test_vcs_section_without_commits(jinja):
    context = _create_context('fake-service', {'builds': []})

    soup = _render(jinja, 'partials/vcs-section.html', context)

    assert 'fake-service-pane' in soup.find('section', class_='pane')['class']
    assert len(soup.find_all('div', class_='pane-item')) == 4


def test_vcs_section_with_commits(jinja):
    commits = [
        _commit('one', 'one day ago', 'Alice'),
        _commit('two', 'two days ago', 'Bob'),
        _commit('three', 'three days ago', 'Chris'),
        _commit('four', 'four days ago', 'Dipak'),
    ]
    context = _create_context('fake-service', {'builds': commits})

    soup = _render(jinja, 'partials/vcs-section.html', context)

    assert 'fake-service-pane' in soup.find('section', class_='pane')['class']
    items = soup.find_all('div', class_='pane-item')
    _assert_contains(items, 'author', ['Alice', 'Bob', 'Chris', 'Dipak'])
    _assert_contains(
        items,
        'committed',
        ['one day ago', 'two days ago', 'three days ago', 'four days ago'],
    )
    _assert_contains(items, 'message', ['one', 'two', 'three', 'four'])


def _assert_contains(items, cls, expected):
    assert [element.find(class_=cls).string for element in items] == expected


def _assert_classes_contain(items, classes):
    for item, cls in zip(items, classes):
        assert cls in item['class']


def _build(outcome, author, elapsed, message):
    return dict(
        outcome=outcome,
        author=author,
        elapsed=elapsed,
        message=message,
    )


def _commit(message, committed, author):
    return dict(message=message, committed=committed, author=author)


def _render(jinja, template, context):
    rendered = jinja.get_template(template).render(context)
    return BeautifulSoup(rendered, 'html.parser')


def _create_context(service_name, service_data=None):
    service_id = 'abc123'
    return dict(
        service_id=service_id,
        service_data=service_data,
        service={'service_name': service_name},
    )
