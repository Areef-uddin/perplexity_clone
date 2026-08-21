import 'package:flutter/material.dart';

import 'package:perplexity_clone/theme/colors.dart';

class SideBarButton extends StatelessWidget {
  final bool isCollapsed;
  final IconData icon;
  final String text;

  const SideBarButton({
    super.key,
    required this.isCollapsed,
    required this.icon,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    if (isCollapsed) {
      return SizedBox(
        height: 50,
        width: double.infinity,
        child: Center(
          child: Icon(
            icon,
            color: AppColors.iconGrey,
            size: 22,
          ),
        ),
      );
    }

    return SizedBox(
      height: 50,
      width: double.infinity,
      child: Row(
        children: [
          const SizedBox(width: 10),

          Icon(
            icon,
            color: AppColors.iconGrey,
            size: 22,
          ),

          const SizedBox(width: 12),

          Expanded(
            child: Text(
              text,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),

          const SizedBox(width: 10),
        ],
      ),
    );
  }
}