using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Weapon", menuName = "InventoryItems/Weapon", order = 1)]
public class Weapon : Item {


	public float fireRate = 1;
	public Sprite gunSprite;
	public Color color;

	public float length;

	public int clipMax;
	public int clipCurrent;

	public enum BulletType
	{
		NineMM,
		FiveSix
	}

	public BulletType bulletType;


	public override void Equip (Pawn pawn)
	{

		pawn.weaponRenderer.sprite = gunSprite;
		pawn.weaponRenderer.color = color;

		pawn.weaponRenderer.enabled = true;

	}

	public override void DeQuip (Pawn pawn)
	{
		
		pawn.weaponRenderer.enabled = false;

		pawn.weaponRenderer.sprite = null;
		pawn.weaponRenderer.color = Color.white;




	}

}
