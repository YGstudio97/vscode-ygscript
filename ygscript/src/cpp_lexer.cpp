/*
 * YGScript C++ - Lexer Implementation
 */

#include "cpp_lexer.hpp"
#include <cctype>
#include <charconv>

namespace ygscript {

Lexer::Lexer(std::string_view src) : source(src) {}

std::vector<Token> Lexer::tokenize() {
    while (pos < source.length()) {
        skip_whitespace();
        
        if (pos >= source.length()) break;
        
        char current_char = peek();
        int start_line = line;
        int start_column = column;
        
        // Numbers
        if (std::isdigit(current_char)) {
            tokens.push_back(read_number());
        }
        // Strings and characters
        else if (current_char == '"' || current_char == '\'') {
            tokens.push_back(read_string());
        }
        // Identifiers and keywords
        else if (std::isalpha(current_char) || current_char == '_') {
            tokens.push_back(read_identifier());
        }
        // Operators and delimiters
        else if (current_char == '+') {
            advance();
            if (peek() == '+') {
                advance();
                add_token(TokenType::INCREMENT, "++");
            } else if (peek() == '=') {
                advance();
                add_token(TokenType::PLUS_ASSIGN, "+=");
            } else {
                add_token(TokenType::PLUS, "+");
            }
        }
        else if (current_char == '-') {
            advance();
            if (peek() == '-') {
                advance();
                add_token(TokenType::DECREMENT, "--");
            } else if (peek() == '=') {
                advance();
                add_token(TokenType::MINUS_ASSIGN, "-=");
            } else if (peek() == '>') {
                advance();
                add_token(TokenType::ARROW, "->");
            } else {
                add_token(TokenType::MINUS, "-");
            }
        }
        else if (current_char == '*') {
            advance();
            if (peek() == '=') {
                advance();
                add_token(TokenType::STAR_ASSIGN, "*=");
            } else {
                add_token(TokenType::STAR, "*");
            }
        }
        else if (current_char == '/') {
            if (peek(1) == '/') {
                skip_comment();
            } else {
                advance();
                if (peek() == '=') {
                    advance();
                    add_token(TokenType::SLASH_ASSIGN, "/=");
                } else {
                    add_token(TokenType::SLASH, "/");
                }
            }
        }
        else if (current_char == '%') {
            advance();
            add_token(TokenType::PERCENT, "%");
        }
        else if (current_char == '=') {
            advance();
            if (peek() == '=') {
                advance();
                add_token(TokenType::EQ, "==");
            } else {
                add_token(TokenType::ASSIGN, "=");
            }
        }
        else if (current_char == '!') {
            advance();
            if (peek() == '=') {
                advance();
                add_token(TokenType::NE, "!=");
            } else {
                add_token(TokenType::NOT, "!");
            }
        }
        else if (current_char == '<') {
            advance();
            if (peek() == '<') {
                advance();
                add_token(TokenType::LSHIFT, "<<");
            } else if (peek() == '=') {
                advance();
                add_token(TokenType::LE, "<=");
            } else {
                add_token(TokenType::LT, "<");
            }
        }
        else if (current_char == '>') {
            advance();
            if (peek() == '>') {
                advance();
                add_token(TokenType::RSHIFT, ">>");
            } else if (peek() == '=') {
                advance();
                add_token(TokenType::GE, ">=");
            } else {
                add_token(TokenType::GT, ">");
            }
        }
        else if (current_char == '&') {
            advance();
            if (peek() == '&') {
                advance();
                add_token(TokenType::AND, "&&");
            } else {
                add_token(TokenType::AMPERSAND, "&");
            }
        }
        else if (current_char == '|') {
            advance();
            if (peek() == '|') {
                advance();
                add_token(TokenType::OR, "||");
            } else {
                add_token(TokenType::BIT_OR, "|");
            }
        }
        else if (current_char == '^') {
            advance();
            add_token(TokenType::BIT_XOR, "^");
        }
        else if (current_char == '~') {
            advance();
            add_token(TokenType::BIT_NOT, "~");
        }
        else if (current_char == '(') {
            advance();
            add_token(TokenType::LPAREN, "(");
        }
        else if (current_char == ')') {
            advance();
            add_token(TokenType::RPAREN, ")");
        }
        else if (current_char == '{') {
            advance();
            add_token(TokenType::LBRACE, "{");
        }
        else if (current_char == '}') {
            advance();
            add_token(TokenType::RBRACE, "}");
        }
        else if (current_char == '[') {
            advance();
            add_token(TokenType::LBRACKET, "[");
        }
        else if (current_char == ']') {
            advance();
            add_token(TokenType::RBRACKET, "]");
        }
        else if (current_char == ';') {
            advance();
            add_token(TokenType::SEMICOLON, ";");
        }
        else if (current_char == ':') {
            advance();
            add_token(TokenType::COLON, ":");
        }
        else if (current_char == ',') {
            advance();
            add_token(TokenType::COMMA, ",");
        }
        else if (current_char == '.') {
            advance();
            add_token(TokenType::DOT, ".");
        }
        else if (current_char == '?') {
            advance();
            add_token(TokenType::QUESTION, "?");
        }
        else {
            error(std::string("Unexpected character: ") + current_char);
        }
    }
    
    add_token(TokenType::EOF_TOKEN, "");
    return tokens;
}

char Lexer::peek(size_t offset) const noexcept {
    if (pos + offset < source.length()) {
        return source[pos + offset];
    }
    return '\0';
}

char Lexer::advance() noexcept {
    if (pos >= source.length()) return '\0';
    char ch = source[pos++];
    if (ch == '\n') {
        line++;
        column = 1;
    } else {
        column++;
    }
    return ch;
}

void Lexer::skip_whitespace() noexcept {
    while (pos < source.length() && std::isspace(peek()) && peek() != '\n') {
        advance();
    }
}

void Lexer::skip_comment() noexcept {
    while (pos < source.length() && peek() != '\n') {
        advance();
    }
}

void Lexer::add_token(TokenType type, std::string_view value) {
    tokens.emplace_back(type, value, line, column);
}

Token Lexer::read_number() {
    int start_line = line;
    int start_column = column;
    std::string num;
    
    while (pos < source.length() && (std::isdigit(peek()) || peek() == '.')) {
        num += advance();
    }
    
    // Check for type suffix
    if (peek() == 'f' || peek() == 'd') {
        char suffix = advance();
        num += suffix;
        return Token(suffix == 'f' ? TokenType::FLOAT : TokenType::DOUBLE, num, start_line, start_column);
    }
    
    if (num.find('.') != std::string::npos) {
        return Token(TokenType::FLOAT, num, start_line, start_column);
    }
    
    return Token(TokenType::INTEGER, num, start_line, start_column);
}

Token Lexer::read_string() {
    int start_line = line;
    int start_column = column;
    char quote = advance();
    std::string str;
    
    while (pos < source.length() && peek() != quote) {
        if (peek() == '\\') {
            advance();
            switch (peek()) {
                case 'n': str += '\n'; break;
                case 't': str += '\t'; break;
                case 'r': str += '\r'; break;
                case '\\': str += '\\'; break;
                case '"': str += '"'; break;
                case '\'': str += '\''; break;
                default: str += peek();
            }
            advance();
        } else {
            str += advance();
        }
    }
    
    if (pos >= source.length()) {
        error("Unterminated string");
    }
    
    advance(); // closing quote
    
    TokenType type = (quote == '"') ? TokenType::STRING : TokenType::CHAR;
    return Token(type, str, start_line, start_column);
}

Token Lexer::read_identifier() {
    int start_line = line;
    int start_column = column;
    std::string ident;
    
    while (pos < source.length() && (std::isalnum(peek()) || peek() == '_')) {
        ident += advance();
    }
    
    auto it = keywords.find(ident);
    TokenType type = (it != keywords.end()) ? it->second : TokenType::IDENTIFIER;
    
    return Token(type, ident, start_line, start_column);
}

void Lexer::error(const std::string& message) {
    throw LexerError(message, line, column);
}

} // namespace ygscript
