import pytest
from lambda_function import InvalidPrefix, generate_new_key


def test_generate_new_key():
    old_key = 'foo/bar/object'
    old_prefix = 'foo/'
    new_prefix = 'hello/world/'
    with pytest.raises(InvalidPrefix):
        generate_new_key(old_key, new_prefix='hello')
    with pytest.raises(InvalidPrefix):
        generate_new_key(old_key, old_prefix='foo', recursive=True)
    assert generate_new_key(old_key) == 'object'
    assert generate_new_key(
        old_key, new_prefix=new_prefix) == 'hello/world/object'
    assert generate_new_key(old_key, new_prefix=new_prefix,
                            recursive=True) == 'hello/world/foo/bar/object'
    # old_prefix only works when recursive set to True.
    assert generate_new_key(old_key, old_prefix=old_prefix) == 'object'
    assert generate_new_key(old_key, new_prefix=new_prefix,
                            old_prefix=old_prefix) == 'hello/world/object'
    assert generate_new_key(old_key, old_prefix=old_prefix,
                            recursive=True) == 'bar/object'
    assert generate_new_key(old_key, new_prefix=new_prefix, old_prefix=old_prefix,
                            recursive=True) == 'hello/world/bar/object'
