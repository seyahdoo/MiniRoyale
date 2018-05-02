using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class KillFeedUI : MonoBehaviour {

	private List<string> KilledTexts = new List<string>();

	[SerializeField] private TextMeshProUGUI text;

	public void KILED(string DeadPlayerName, string KillerPlayerName, string CauseOfDeath){

		text.text += KillerPlayerName + " killed " + DeadPlayerName + " with " + CauseOfDeath +"\n";

	}



}
