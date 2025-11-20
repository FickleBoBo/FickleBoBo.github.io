package basic;

public class Main {

    public static void main(String[] args) {
        for (Ensemble e : Ensemble.values()) {
            System.out.println(e + " = " + e.numberOfMusicians());
            // 출력 결과
            // SOLO = 1
            // DUET = 2
            // TRIO = 3
            // QUARTET = 4
            // QUINTET = 5
            // SEXTET = 6
            // SEPTET = 7
            // OCTET = 8
            // NONET = 9
            // DECTET = 10
        }
    }
}
