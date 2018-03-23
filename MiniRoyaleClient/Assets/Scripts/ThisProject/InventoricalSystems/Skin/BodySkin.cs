using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Skin", menuName = "InventoryItems/Skin/BodySkin", order = 1)]
public class BodySkin : Skin {

	public Sprite sprite;
	public Sprite deQuipSprite;


	public Color color;
	public Color deQuipColor;

	public override void Equip (Pawn pawn)
	{
		Debug.Log ("Equipping: " + name);

		pawn.bodyRenderer.sprite = sprite;
		pawn.bodyRenderer.color = color;

		pawn.bodyRenderer.enabled = true;

	}


	public override void DeQuip (Pawn pawn)
	{
		pawn.bodyRenderer.enabled = false;

		pawn.bodyRenderer.sprite = deQuipSprite;
		pawn.bodyRenderer.color = deQuipColor;


	}

}
