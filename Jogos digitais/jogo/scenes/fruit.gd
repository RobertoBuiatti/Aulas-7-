extends Node2D

class_name Fruit

#Fruta comida
signal fruit_eaten

func _ready() -> void:
	pass
	
func _process(delta: float) -> void:
	pass

func _on_area_2d_body_entered(body: Node2D) -> void:
	fruit_eaten.emit()#emitindo o sinal
	queue_free() #remove a fruta
