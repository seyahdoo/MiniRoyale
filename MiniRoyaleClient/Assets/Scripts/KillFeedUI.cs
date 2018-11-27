using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class KillFeedUI : MonoBehaviour {

	//private List<string> KilledTexts = new List<string>();

	[SerializeField] private TextMeshProUGUI text;

    public AnimationCurve fadeCurve;
    public float feedTotalScreenTime;

    public List<KillFeedMember> members = new List<KillFeedMember>();

    private void Update()
    {
        text.text = "";

        foreach (KillFeedMember m in members)
        {
            int h = (int)(255 * fadeCurve.Evaluate((Time.time - m.startTime)/feedTotalScreenTime));
            string ht = h.ToString("X2");
            text.text += "<alpha=#"+ht+">";
            text.text += m.text;
        }

        for (int i = members.Count-1; i >= 0; i--)
        {
            if(((Time.time - members[i].startTime) / feedTotalScreenTime) >= 1)
            {
                members.RemoveAt(i);
            }

        }
    }

    public void KILED(string DeadPlayerName, string KillerPlayerName, string CauseOfDeath){

        KillFeedMember kfm = new KillFeedMember
        {
            text = KillerPlayerName + " killed " + DeadPlayerName + " with " + CauseOfDeath + "\n",
            startTime = Time.time
        };

        members.Add(kfm);

    }

    public class KillFeedMember
    {
        public string text;
        public float startTime;
    }

}
