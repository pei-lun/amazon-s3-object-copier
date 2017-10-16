import pytest

from lambda_function import InvalidPrefix, generate_new_key


def test_generate_new_key():
    old_key = 'bar/baz/object'
    skip = 'bar/'
    new_prefix = 'foo/'
    invalid_prefix = 'foo'
    with pytest.raises(InvalidPrefix):
        generate_new_key(old_key, prefix=invalid_prefix)
    with pytest.raises(InvalidPrefix):
        generate_new_key(old_key, recursive=True, skip=invalid_prefix)
    assert generate_new_key(old_key) == 'object'
    assert generate_new_key(
        old_key, prefix=new_prefix) == 'foo/object'
    assert generate_new_key(old_key, prefix=new_prefix,
                            recursive=True) == 'foo/bar/baz/object'
    # skip argument only works when recursive argument set to True.
    assert generate_new_key(old_key, skip=skip) == 'object'
    assert generate_new_key(old_key, prefix=new_prefix,
                            skip=skip) == 'foo/object'
    assert generate_new_key(old_key, recursive=True, skip=skip) == 'baz/object'
    assert generate_new_key(old_key, prefix=new_prefix, recursive=True,
                            skip=skip) == 'foo/baz/object'
