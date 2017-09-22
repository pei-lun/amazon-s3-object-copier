import pytest

from lambda_function import InvalidPrefix, generate_new_key


def test_generate_new_key():
    old_key = 'foo/bar/object'
    skip = 'foo/'
    new_prefix = 'hello/world/'
    with pytest.raises(InvalidPrefix):
        generate_new_key(old_key, prefix='hello')
    with pytest.raises(InvalidPrefix):
        generate_new_key(old_key, recursive=True, skip='foo')
    assert generate_new_key(old_key) == 'object'
    assert generate_new_key(
        old_key, prefix=new_prefix) == 'hello/world/object'
    assert generate_new_key(old_key, prefix=new_prefix,
                            recursive=True) == 'hello/world/foo/bar/object'
    # skip argument only works when recursive argument set to True.
    assert generate_new_key(old_key, skip=skip) == 'object'
    assert generate_new_key(old_key, prefix=new_prefix,
                            skip=skip) == 'hello/world/object'
    assert generate_new_key(old_key, recursive=True, skip=skip) == 'bar/object'
    assert generate_new_key(old_key, prefix=new_prefix, recursive=True,
                            skip=skip) == 'hello/world/bar/object'
