package pro.demo.springrequest;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @PostMapping
    public ResponseEntity<String> createUser(@Valid @RequestBody UserRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body("User created: " + request.getName());
    }

    @GetMapping("/{userId}")
    public ResponseEntity<String> getUser(@PathVariable Long userId) {
        return ResponseEntity.ok("User ID: " + userId);
    }
}