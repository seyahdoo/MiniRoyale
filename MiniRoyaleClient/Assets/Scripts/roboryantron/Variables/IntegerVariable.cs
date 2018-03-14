using UnityEngine;

namespace RoboRyanTron.Unite2017.Variables
{
	[CreateAssetMenu]
	public class IntegerVariable : ScriptableObject
	{
		#if UNITY_EDITOR
		[Multiline]
		public string DeveloperDescription = "";
		#endif
		public int Value;

		public void SetValue(int value)
		{
			Value = value;
		}

		public void SetValue(IntegerVariable value)
		{
			Value = value.Value;
		}

		public void ApplyChange(int amount)
		{
			Value += amount;
		}

		public void ApplyChange(IntegerVariable amount)
		{
			Value += amount.Value;
		}
	}
}