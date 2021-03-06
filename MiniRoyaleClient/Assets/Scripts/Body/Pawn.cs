﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading;

public class Pawn : MonoBehaviour {

	public string PlayerName;

    public bool isDead;
    public Sprite DeadSprite;

	public SpriteRenderer bodyRenderer; 
	public SpriteRenderer weaponRenderer;
    public GameObject EyeL;
    public GameObject EyeR;


	public Dictionary<int,Item> inventory = new Dictionary<int,Item>();


	Queue<UniqueItem> EquipItemQueue = new Queue<UniqueItem>();
	Queue<UniqueItem> DeEquipItemQueue = new Queue<UniqueItem>();


	void Update(){

		while (EquipItemQueue.Count > 0) {
			EquipSpcial (EquipItemQueue.Dequeue ());
		}

		while (DeEquipItemQueue.Count > 0) {
			DeQuip (DeEquipItemQueue.Dequeue ());
		}

	}

	public void EquipSpcial(UniqueItem item){
		//Debug.Log ("Equipped: " + item);
		//Debug.Log ("Current thread: "+Thread.CurrentThread.Name);


		item.item.Equip(this);
		//inventory.Add (item.id,item.item);
	}

	public void EquipThreadSafe(UniqueItem item){
		//Debug.Log ("Equipped Thread Safe: " + item);

		//Debug.Log ("Current thread: "+Thread.CurrentThread.Name);
		EquipItemQueue.Enqueue (item);
	}

	public void DeQuip(UniqueItem item){
		item.item.DeQuip (this);
		inventory.Remove (item.id);
	}

	public void DeQuipThreadSafe(UniqueItem item){
		DeEquipItemQueue.Enqueue (item);
	}

    public void Killed() {

        isDead = true;

        bodyRenderer.sprite = DeadSprite;
        weaponRenderer.sprite = null;
        EyeL.SetActive(false);
        EyeR.SetActive(false);

    }

}
