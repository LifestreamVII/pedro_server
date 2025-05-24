using System.Collections.Generic;
using System.IO;
using PKHeX.Core;
using System.Text.Json;
using System.Security.Cryptography;
using System.Xml.Linq;
using System.Xml;
using Newtonsoft.Json;
using System.Text;

public static class SavePkmHelper
{
    private static readonly string SaveFilePath = Path.Combine(Directory.GetCurrentDirectory(), "savedata.sav");
    private static readonly string TextFilePath = Path.Combine(Directory.GetCurrentDirectory(), "data.txt");
    private static readonly string PkmTemplatePath = Path.Combine(Directory.GetCurrentDirectory(), "template.pk5");

    public static void ReadSaveData(string filePath)
    {
        // Look for the save file saved at the given location
        var sav = SaveUtil.GetVariantSAV(filePath);

        // Create a dictionary for trainer data
        var trainerData = new Dictionary<string, object>
            {
                { "Gen", sav.Generation },
                { "PlayTime", sav.PlayTimeString },
                { "Name", sav.OT },
                { "Gender", sav.Gender },
                { "ID32", sav.ID32 },
                { "SID7", sav.TrainerSID7},
                { "TID7", sav.TrainerTID7},
                { "Version", sav.Version}
            };

        // Serialized JSON string of trainer data
        string trainerString = JsonConvert.SerializeObject(trainerData, Newtonsoft.Json.Formatting.Indented);

        File.WriteAllText("trainer.txt", trainerString);

        int counter = 0; // Initialize counter

        foreach (var poke in sav.BoxData)
        {
            counter++; // Increment counter

            var pobj = new Dictionary<string, object>
                {
                    { "Species", poke.Species },
                    { "Name", poke.Nickname },
                    { "Level", poke.CurrentLevel },
                    { "Sex", poke.Gender },
                    { "Box", counter },
                    { "Ball", poke.Ball },
                    { "Friendship", poke.CurrentFriendship },
                    { "Trainer", poke.OriginalTrainerName },
                    { "Version", poke.Version },
                    { "Data", poke.Data },
                };

            // Serialized JSON string of trainer data
            string boxString = JsonConvert.SerializeObject(pobj, Newtonsoft.Json.Formatting.Indented);

            File.WriteAllText("box"+counter+".txt", boxString);

            if (counter >= 10) // Check if counter exceeds 20
                break; // Exit the loop
        }

        Console.Write("DEC_OK");
    }

    public static void WriteSaveData(string savePath, string pkmPath, int gen, int boxIndex)
    {
        // Look for the save file saved at the given location
        var sav = SaveUtil.GetVariantSAV(savePath);

        bool genDiff = sav.Generation != gen;
        
        var all = sav.BoxData;

        // Look for the saved pkm file at the given location
        PKM pkm = gen switch
        {
            4 => new PK4(File.ReadAllBytes(pkmPath)),
            5 => new PK5(File.ReadAllBytes(pkmPath)),
            _ => new PK5(File.ReadAllBytes(pkmPath))
        };

        if (genDiff)
        {
            var pk4 = new PK4(File.ReadAllBytes("PK4TEMPLATE.pk4"));
            pk4.Species = pkm.Species;
            pk4.CurrentLevel = pkm.CurrentLevel;
            var rnd = new System.Random();
            EntityPID.GetRandomPID(rnd, pkm.Species, pkm.Gender, pk4.Version, pkm.Nature, pkm.Form, pkm.PID);
            pk4.SID16 = pkm.SID16;
            pk4.TID16 = pkm.TID16;
            pk4.TrainerSID7 = pkm.TrainerSID7;
            pk4.TrainerTID7 = pkm.TrainerTID7;
            pk4.OriginalTrainerGender = pkm.OriginalTrainerGender;
            pk4.OriginalTrainerName = pkm.OriginalTrainerName;
            pk4.AbilityNumber = pkm.AbilityNumber;
            pk4.Ball = pkm.Ball;
            pk4.CurrentFriendship = pkm.CurrentFriendship;
            pk4.DisplaySID = pkm.DisplaySID;
            pk4.DisplayTID = pkm.DisplayTID;
            pk4.Gender = pkm.Gender;
            pk4.Language = pkm.Language;
            pk4.MetDate = pkm.MetDate;
            pk4.MetLevel = pkm.MetLevel;
            pk4.Moves = pkm.Moves;
            pk4.Nickname = pkm.Nickname;
            pk4.Nature = pkm.Nature;

            all[boxIndex] = pk4;

        }
        else
        {
            all[boxIndex] = pkm;
        }

        sav.BoxData = all;

        File.WriteAllBytes(savePath, sav.Write());
    }

    public static void DecodePkm(string filePath, int gen)
    {
        // Look for the saved pkm file at the given location
        PKM pkm = gen switch
        {
            4 => new PK4(File.ReadAllBytes(filePath)),
            5 => new PK5(File.ReadAllBytes(filePath)),
            _ => new PK5(File.ReadAllBytes(filePath))
        };

        var pobj = new Dictionary<string, object>
            {
                { "Species", pkm.Species },
                { "Name", pkm.Nickname },
                { "Level", pkm.CurrentLevel },
                { "Sex", pkm.Gender },
                { "Ball", pkm.Ball },
                { "Friendship", pkm.CurrentFriendship },
                { "Trainer", pkm.OriginalTrainerName },
                { "Version", pkm.Version },
                //{ "Data", pkm.Data },
            };

        string pkmData = JsonConvert.SerializeObject(pobj, Newtonsoft.Json.Formatting.Indented);

        Console.Write(pkmData);
    }
}