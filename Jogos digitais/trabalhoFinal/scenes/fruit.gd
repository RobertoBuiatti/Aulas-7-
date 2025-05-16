extends Node2D

class_name Fruit

@onready var animation_player: AnimationPlayer = $AnimationPlayer
#Fruta comida
signal fruit_eaten(quantity)

func _ready() -> void:
	pass
	
func _process(delta: float) -> void:
	if not animation_player.is_playing() or animation_player.current_animation != "idle":
		animation_player.play("idle")

func _on_area_2d_body_entered(body: Node2D) -> void:
	fruit_eaten.emit(1)#emitindo o sinal
	queue_free() #remove a fruta
