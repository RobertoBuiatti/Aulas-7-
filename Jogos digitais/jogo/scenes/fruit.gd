extends Node2D


func _ready() -> void:
	pass
	
func _process(delta: float) -> void:
	pass

func _on_area_2d_body_entered(body: Node2D) -> void:
	print("pegou fruta")
	queue_free() #remove a fruta
