using System;

namespace PkmSaveOperations
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length < 2)
            {
                Console.WriteLine("Usage: PkmSaveOperations <path_to_save_file> <method_flag>");
                return;
            }

            string methodFlag = args[0];
            string filePath = args[1];

            if (methodFlag == "readsave")
            {
                SavePkmHelper.ReadSaveData(filePath);
            }
            else if (methodFlag == "decpkm")
            {
                int genFlag = Int32.Parse(args[2]);
                SavePkmHelper.DecodePkm(filePath, genFlag);
            }
            else if (methodFlag == "writesave")
            {
                string pkmPath = args[2];
                int genFlag = Int32.Parse(args[3]);
                int boxFlag = Int32.Parse(args[4]);
                SavePkmHelper.WriteSaveData(filePath, pkmPath, genFlag, boxFlag);
            }
            else
            {
                Console.WriteLine("Invalid method flag. Please use 'readsave' or 'decpkm'.");
            }
        }
    }
}
