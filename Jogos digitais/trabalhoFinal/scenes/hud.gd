extends CanvasLayer

@onready var label: Label = $MarginContainer/HBoxContainer/Label


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func eat_fruit(quantity):
	var actual = int(label.text)
	actual += quantity
	label.text = str(actual)
