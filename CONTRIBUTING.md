# Contributing to Duplicate Check Service

Cảm ơn bạn đã quan tâm đến việc đóng góp cho dự án này!

## Cách Đóng Góp

### Báo Cáo Bug

1. Kiểm tra xem bug đã được báo cáo chưa trong [Issues](https://github.com/your-repo/issues)
2. Tạo issue mới với:
   - Mô tả chi tiết về bug
   - Các bước để tái tạo bug
   - Thông tin về môi trường (OS, Python version, etc.)
   - Screenshot nếu có thể

### Đề Xuất Tính Năng

1. Kiểm tra xem tính năng đã được đề xuất chưa
2. Tạo issue mới với:
   - Mô tả chi tiết về tính năng
   - Lý do tại sao tính năng này hữu ích
   - Cách sử dụng dự kiến

### Đóng Góp Code

1. Fork repository
2. Tạo branch mới cho feature/fix:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Thực hiện thay đổi
4. Thêm tests cho code mới
5. Chạy tests để đảm bảo mọi thứ hoạt động:
   ```bash
   pytest tests/ -v
   ```
6. Commit changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
7. Push to branch:
   ```bash
   git push origin feature/amazing-feature
   ```
8. Tạo Pull Request

## Coding Standards

### Python Code Style

- Tuân thủ PEP 8
- Sử dụng type hints
- Viết docstrings cho functions và classes
- Giữ functions ngắn gọn và dễ đọc

### Testing

- Viết tests cho mọi tính năng mới
- Đảm bảo coverage > 80%
- Sử dụng descriptive test names
- Mock external dependencies

### Documentation

- Cập nhật README.md nếu cần
- Thêm comments cho code phức tạp
- Cập nhật API documentation

## Pull Request Guidelines

1. **Title**: Mô tả ngắn gọn về thay đổi
2. **Description**: 
   - Mô tả chi tiết về thay đổi
   - Link đến issue liên quan
   - Screenshots nếu có UI changes
3. **Tests**: Đảm bảo tất cả tests pass
4. **Documentation**: Cập nhật docs nếu cần

## Code Review Process

1. Tất cả PRs sẽ được review
2. Maintainers sẽ review và comment
3. Address feedback và update PR
4. PR sẽ được merge khi approved

## Getting Help

- Tạo issue với label "question"
- Join our discussions
- Check existing documentation

Cảm ơn bạn đã đóng góp! 🎉 