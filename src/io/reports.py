

def save_squat_report(evaluated_squats, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("RAPORT ANALIZY PRZYSIADÓW\n")
        f.write("========================\n\n")

        for i, squat in enumerate(evaluated_squats, start=1):
            status = "POPRAWNY" if squat["valid"] else "NIEPOPRAWNY"
            comment = squat_comment(squat)

            f.write(f"Przysiad #{i}\n")
            f.write(f"Status: {status}\n")
            f.write(f"Komentarz: {comment}\n\n")

            if not squat["valid"]:
                f.write("Błędy:\n")
                for err in squat["errors"]:
                    f.write(f" - {err}\n")
                f.write("\n")

            f.write(f"min kąt kolana: {squat['min_knee']:.1f}°\n")
            f.write(f"max pochylenie tułowia: {squat['max_trunk']:.1f}°\n")
            f.write(f"tempo (dół/góra): {squat['tempo_ratio']:.2f}\n")
            f.write("\n\n")

def squat_comment(squat):
    if squat["valid"]:
        return "Bardzo dobry przysiad - dobra głębokość i kontrola tułowia"
    
    if "Zbyt płytki przysiad" in squat["errors"]:
        return "Spróbuj zejść niżej - brakuje głębokości"
    
    if "Zbyt duże pochylenie tułowia" in squat["errors"]:
        return "Utrzymuj bardziej wyprostowany tułów"
    
    return "Przysiad do poprawy - zwróć uwagę na technikę"