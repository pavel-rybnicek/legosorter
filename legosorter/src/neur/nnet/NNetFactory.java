package neur.nnet;

public class NNetFactory
{
  public enum NNetType
  {
    NEUROPH;
  }
  
  
  public static INNet getNNet (NNetType nnetType)
  {
    switch (nnetType)
    {
    case NEUROPH:
      return new NeurophNNet ();
    }
    
    return null;
  }

}
