extends Node2D
@onready var timer: Timer = $Timer
@onready var sprite_2d: Sprite2D = $Sprite2D
var phases: int = 0

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	timer.start()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_timer_timeout() -> void:
	if phases < 3:
		sprite_2d.frame += 1
		phases += 1
	else:
		timer.stop()
		
