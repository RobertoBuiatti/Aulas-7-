extends Node2D

class_name Fruit_Random

#Fruta comida
signal fruit_eaten(quantity)

@export var list_fruits: Array[Texture2D]
@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var animation_player: AnimationPlayer = $AnimationPlayer


func _ready() -> void:
	var n = randi_range(0, list_fruits.size() - 1)
	sprite_2d.texture = list_fruits[n]
	
	
func _process(delta: float) -> void:
	if not animation_player.is_playing() or animation_player.current_animation != "idle":
		animation_player.play("idle")

func _on_area_2d_body_entered(body: Node2D) -> void:
	fruit_eaten.emit(2)#emitindo o sinal
	queue_free() #remove a fruta
