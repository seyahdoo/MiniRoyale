// ----------------------------------------------------------------------------
// Unite 2017 - Game Architecture with Scriptable Objects
// 
// Author: Ryan Hipple
// Date:   10/04/17
// ----------------------------------------------------------------------------

using System;

namespace RoboRyanTron.Unite2017.Variables
{
	[Serializable]
	public class IntegerReference
	{
		public bool UseConstant = true;
		public int ConstantValue;
		public IntegerVariable Variable;

		public IntegerReference()
		{ }

		public IntegerReference(int value)
		{
			UseConstant = true;
			ConstantValue = value;
		}

		public int Value
		{
			get { return UseConstant ? ConstantValue : Variable.Value; }
		}

		public static implicit operator int(IntegerReference reference)
		{
			return reference.Value;
		}
	}
}