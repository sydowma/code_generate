package pro.novai.springrequest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void testCreateUser_ValidRequest() throws Exception {
        String VALID_JSON = """
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "age": 25
                }
                """;
        mockMvc.perform(post("/api/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(VALID_JSON))
                .andExpect(status().isCreated())
                .andExpect(content().string("User created: John Doe"));
    }

    @Test
    void testCreateUser_InvalidRequest() throws Exception {
        String invalidJson = """
        {
            "name": " ",
            "email": "invalid-email",
            "age": 17
        }
        """;

        mockMvc.perform(post("/api/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(invalidJson))
                .andExpect(status().isBadRequest());
    }

    @Test
    void testGetUser_ValidId() throws Exception {
        mockMvc.perform(get("/api/users/123"))
                .andExpect(status().isOk())
                .andExpect(content().string("User ID: 123"));
    }

    @Test
    void testGetUser_InvalidId() throws Exception {
        mockMvc.perform(get("/api/users/abc")) // 非数字ID
                .andExpect(status().isBadRequest());
    }
}