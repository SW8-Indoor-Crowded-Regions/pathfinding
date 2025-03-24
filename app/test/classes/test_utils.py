from app.classes.utils import dict_to_obj


class TestUtils:
    def test_dict_to_obj_with_nested_dict(self):
        data = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        obj = dict_to_obj(data)
        # Verify nested attributes.
        assert obj.a == 1
        assert obj.b.c == 2
        assert obj.b.d.e == 3

    def test_dict_to_obj_with_list_of_dicts(self):
        data = [{'a': 1}, {'b': 2}]
        obj = dict_to_obj(data)
        assert obj[0].a == 1
        assert obj[1].b == 2

    def test_dict_to_obj_with_non_dict(self):
        data = 'test string'
        result = dict_to_obj(data)
        # Non-dict/list input should be returned as-is.
        assert result == 'test string'
