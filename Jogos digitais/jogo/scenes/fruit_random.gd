extends Node2D

class_name Fruit_Random

#Fruta comida
signal fruit_eaten

@export var list_fruits: Array[Texture2D]
@onready var sprite_2d: Sprite2D = $Sprite2D


func _ready() -> void:
	var n = randi_range(0, list_fruits.size() - 1)
	sprite_2d.texture = list_fruits[n]
	
	
func _process(delta: float) -> void:
	pass

func _on_area_2d_body_entered(body: Node2D) -> void:
	fruit_eaten.emit()#emitindo o sinal
	queue_free() #remove a fruta
