class TileAnimation:
    def __init__(self, start_id, end_id, tile_time):
        self.start_id = start_id
        self.end_id = end_id 
        self.tile_time = tile_time
        self.timer = 0
        self.frame_id = start_id

    def update(self, deltaTime, entity) -> int:
        self.timer += deltaTime
        if self.timer >= self.tile_time:
            self.frame_id += 1
            if self.frame_id > self.end_id:
                self.frame_id = self.start_id
            self.timer = 0
        return self.frame_id

    def reset(self):
        self.frame_id = self.start_id
        self.timer = 0