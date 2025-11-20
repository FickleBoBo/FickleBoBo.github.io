import java.io.*;
import java.util.*;

public class Anagrams1 {
    public static void main(String[] args) throws FileNotFoundException {
        File dictionary = new File("./data/data.dat");
        int minGroupSize = 2;

        Map<String, Set<String>> groups = new HashMap<>();
        try (Scanner s = new Scanner(dictionary)) {
            while (s.hasNext()) {
                String word = s.next();

                // computeIfAbsent는 key가 있으면 값을 반환하고 key가 없으면 Function 실행
                groups.computeIfAbsent(alphabetize(word), (unused) -> new TreeSet<>()).add(word);
            }
        }

        // minGroupSize 이상인 그룹 출력
        for (Set<String> group : groups.values()) {
            if (group.size() >= minGroupSize) {
                System.out.println(group.size() + ": " + group);
            }
        }

        // 출력 결과
        // 3: [cdd, dcd, ddc]
        // 2: [aab, aba]
        // 3: [asdf, fasd, sadf]
    }

    // 문자열 s의 알파벳을 오름차순으로 정렬한 애너그램을 반환
    private static String alphabetize(String s) {
        char[] a = s.toCharArray();
        Arrays.sort(a);
        return new String(a);
    }
}
