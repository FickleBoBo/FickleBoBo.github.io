import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

import static java.util.stream.Collectors.groupingBy;

public class Anagrams2 {
    public static void main(String[] args) throws IOException {
        Path dictionary = Paths.get("./data/data.dat");
        int minGroupSize = 2;

        try (Stream<String> words = Files.lines(dictionary)) {
            words.collect(
                            groupingBy(word -> word.chars().sorted()
                                    .collect(StringBuilder::new,
                                            (sb, c) -> sb.append((char) c),
                                            StringBuilder::append).toString()))
                    .values().stream()
                    .filter(group -> group.size() >= minGroupSize)
                    .map(group -> group.size() + ": " + group)
                    .forEach(System.out::println);
        }

        // 출력 결과
        // 3: [cdd, ddc, dcd]
        // 2: [aab, aba]
        // 3: [asdf, fasd, sadf]
    }
}
