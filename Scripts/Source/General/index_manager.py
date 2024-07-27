class IndexManager:
    global_index = 1
    unused_indices = []

    @staticmethod
    def get_id():
        id = IndexManager.global_index
        IndexManager.global_index += 1
        return id

    @staticmethod
    def get_color_by_id(id: int):
        if id > 256 * 256 * 256:
            return 1, 1, 1
        r = id % 256
        g = (id // 256) % 256
        b = ((id // 256) // 256) % 256
        return r / 256.0, g / 256.0, b / 256.0

        # OLD
        # t = id / 255
        # r, g, b = 0, 0, 0
        # if t < 1:
        #     r = t
        # if 1 <= t < 2:
        #     r = 1
        #     g = (id - 255) / 255
        # if 2 <= t:
        #     r, g = 1, 1
        #     b = min((id - 255 * 2) / 255, 1)
        # return r, g, b

    @staticmethod
    def get_id_by_color(color: tuple):
        return int(color[0] * 256) + int(color[1] * 256) * 256 + int(color[2] * 256) * 256 * 256

        # OLD
        # return color[0] * 255 + color[1] * 255 + color[2] * 255
