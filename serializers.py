import json


class CategorySerializer:
    def __init__(self, category_object):
        try:
            if category_object.__len__:
                dict_list = []
                for obj in category_object:
                    temp_dict = {
                        'id': obj.id,
                        'name': obj.name
                    }
                    dict_list.append(temp_dict)
                self.data = json.dumps(dict_list)
        except AttributeError:
            posts_list = []
            if category_object.posts:
                for post in category_object.posts:
                    posts_list.append(PostSerializer(post).post_dict)

                self.data = json.dumps(0)
            category_dict = {
                'id': category_object.id,
                'name': category_object.name,
                'posts': posts_list
            }
            self.data = json.dumps(category_dict)


class PostSerializer:
    def __init__(self, post_object):
        try:
            if post_object.__len__:
                self.post_list = []
                for obj in post_object:
                    temp_dict = {
                        'id': obj.id,
                        'title': obj.title,
                        'body': obj.body,
                        'url': obj.url,
                        'image_url': obj.image_url,
                        'iframe': obj.iframe,
                    }
                    self.post_list.append(temp_dict)
                self.data = json.dumps(self.post_list)
        except AttributeError:
            self.post_dict = {
                'id': post_object.id,
                'title': post_object.title,
                'body': post_object.body,
                'url': post_object.url,
                'image_url': post_object.image_url,
                'iframe': post_object.iframe,
            }
            self.data = json.dumps(self.post_dict)
